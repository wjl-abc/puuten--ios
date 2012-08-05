//
//  BSViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-5.
//
//

#import "BSViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"

@interface BSViewController ()

@end

@implementation BSViewController
@synthesize name=_name;
@synthesize tags=_tags;
@synthesize introduction = _introduction;
@synthesize bs_id;
@synthesize avatar = _avatar;

- (void)setName:(UILabel *)name{
    _name = name;
}

- (void)setTags:(UITextView *)tags{
    _tags = tags;
}

- (void)setIntroduction:(UITextView *)introduction{
    _introduction = introduction;
}

- (void)setAvatar:(UIImageView *)avatar{
    _avatar = avatar;
}

- (void)loadData{
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/bs_weibo_list/%d/", bs_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *bsURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:bsURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        //bsdata = json;
        _name.text = [json objectForKey:@"name"];
        _tags.text = [json objectForKey:@"tags"];
        _introduction.text = [json objectForKey:@"introduction"];
        NSLog(@"%@", [json objectForKey:@"name"]);
        //NSLog(@"%@", [json objectForKey:@"avatar_url"]);
        NSURL *imageURL = [NSURL URLWithString:[json objectForKey:@"avatar_url"]];
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
    _name.text = [NSString stringWithFormat:@"%d", bs_id];
    [super viewDidLoad];
	// Do any additional setup after loading the view.
}

- (void)viewDidAppear:(BOOL)animated
{
    [self loadData];
    [super viewDidAppear:animated];
}

- (void)viewDidUnload
{
    //[self setBs_id:nil];
    [self setName:nil];
    [self setAvatar:nil];
    [self setTags:nil];
    [self setIntroduction:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
