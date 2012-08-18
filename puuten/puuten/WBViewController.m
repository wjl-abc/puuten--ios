//
//  WBViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "WBViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
#import "BSViewController.h"
@interface WBViewController ()

@end

@implementation WBViewController
@synthesize name;
@synthesize bodyField;
@synthesize avatar=_avatar;
@synthesize bsdata;
@synthesize wb_id=_wb_id;
@synthesize bs_id;

- (void)setWb_id:(int)wb_id
{
    _wb_id = wb_id;
}


- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier isEqualToString:@"bsdetails"]) {
        BSViewController *bs = (BSViewController *)segue.destinationViewController;
        bs.bs_id = bs_id;
    }
}

- (void)loadData{
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/wb/%d/", _wb_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *wbURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:wbURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        bsdata = json;
        name.text = [bsdata objectForKey:@"name"];
        bodyField.text = [bsdata objectForKey:@"body"];
        bs_id = [[bsdata objectForKey:@"bs_id"] intValue];
        NSURL *imageURL = [NSURL URLWithString:[bsdata objectForKey:@"avatar_url"]];
        NSData* data = [[NSData alloc] initWithContentsOfURL:imageURL];
        _avatar.image = [UIImage imageWithData:data];
    }];
    [request setFailedBlock:^{
        
    }];
    
    [request startAsynchronous];
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    self.view.frame= CGRectMake(0, 0, 300, 400);
}

- (void)viewDidUnload
{
    [self setName:nil];
    [self setBodyField:nil];
    [self setAvatar:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (void)viewDidAppear:(BOOL)animated
{
    [self loadData];
    [super viewDidAppear:animated];
}



- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)bSHeader:(BSHeader *)sender setName:(NSString *)name_string setAvatar_url:(NSString *)avatar_url
{
    name_string = [bsdata objectForKey:@"name"];
    avatar_url = [bsdata objectForKey:@"avatar_url"];
}

- (IBAction)click:(id)sender {
    [self performSegueWithIdentifier:@"bsdetails" sender:self];
}
@end
