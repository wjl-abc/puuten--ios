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
//@synthesize name;
@synthesize bodyField;
//@synthesize avatar=_avatar;
@synthesize pic=_pic;
@synthesize bsHeader;
@synthesize re_wb;
@synthesize re_view;
@synthesize bsdata;
@synthesize wb_id=_wb_id;
@synthesize bs_id;
@synthesize arrayImg = _arrayImg;
@synthesize order = _order;

- (void)setWb_id:(int)wb_id
{
    _wb_id = wb_id;
}

- (void)setArrayImg:(NSMutableArray *)arrayImg{
    _arrayImg = [[NSMutableArray alloc] init];
    _arrayImg = arrayImg;
}

- (void)setOrder:(int)order{
    _order = order;
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier isEqualToString:@"bsdetails"]) {
        NSLog(@"nnnn");
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
        CGSize constraint = CGSizeMake(280.0f, 400.0f);
        CGSize size_body = [[bsdata objectForKey:@"body"] sizeWithFont:[UIFont systemFontOfSize:14.0f] constrainedToSize:constraint lineBreakMode:UILineBreakModeWordWrap];
        bodyField.lineBreakMode = UILineBreakModeWordWrap;
        bodyField.numberOfLines = 0;
        [bodyField setMinimumFontSize:14.0f];
        bodyField.frame = CGRectMake(20, 90, 280, size_body.height);
        [bodyField setFont:[UIFont systemFontOfSize:14.0f]];
        bodyField.text = [bsdata objectForKey:@"body"];
        bs_id = [[bsdata objectForKey:@"bs_id"] intValue];
        self.bsHeader.bs_id=bs_id;
        int type = [[bsdata objectForKey:@"type"] intValue];
        if (type==1) {
            //NSURL *pic_URL = [NSURL URLWithString:[bsdata objectForKey:@"pic_url"]];
            //NSData* data = [[NSData alloc] initWithContentsOfURL:pic_URL];
            //UIImage *image = [[UIImage alloc] initWithData:data];
            NSLog(@"the clicked order is %i", _order);
            NSLog(@"the length of arrayImg is %i", [_arrayImg count]);
            UIImage *image = [_arrayImg objectAtIndex:_order];
            _pic.frame = CGRectMake(40, 100+size_body.height, 240, 240*image.size.height/image.size.width);
            [_pic setImage:image];
        }
        else if(type==2)
        {
            NSString *re_wb_body = [bsdata objectForKey:@"re_wb_body"];
            NSString *re_wb_name = [bsdata objectForKey:@"re_wb_name"];
            NSString *re_wb_for_display = [NSString stringWithFormat:@"%@: %@", re_wb_name, re_wb_body];
            CGSize constraint = CGSizeMake(260.0f, 400.0f);
            CGSize size_re_wb = [re_wb_for_display sizeWithFont:[UIFont systemFontOfSize:14.0f] constrainedToSize:constraint lineBreakMode:UILineBreakModeWordWrap];
            re_wb.lineBreakMode = UILineBreakModeWordWrap;
            re_wb.numberOfLines = 0;
            [re_wb setMinimumFontSize:14.0f];
            re_wb.frame = CGRectMake(30, size_body.height+100, 260, size_re_wb.height);
            [re_wb setFont:[UIFont systemFontOfSize:14.0f]];
            re_wb.text = re_wb_for_display;
            _pic.frame= CGRectZero;
            re_view.frame = CGRectZero;
            //re_view.frame = CGRectMake(20, size_body.height+100, 280, size_re_wb.height);
            //re_view.backgroundColor = [UIColor colorWithRed:0.94 green:0.94 blue:0.94 alpha:1];
        }
        else if(type==3)
        {
            NSString *re_wb_body = [bsdata objectForKey:@"re_wb_body"];
            NSString *re_wb_name = [bsdata objectForKey:@"re_wb_name"];
            NSString *re_wb_for_display = [NSString stringWithFormat:@"%@: %@", re_wb_name, re_wb_body];
            CGSize constraint = CGSizeMake(260.0f, 400.0f);
            CGSize size_re_wb = [re_wb_for_display sizeWithFont:[UIFont systemFontOfSize:14.0f] constrainedToSize:constraint lineBreakMode:UILineBreakModeWordWrap];
            re_wb.lineBreakMode = UILineBreakModeWordWrap;
            re_wb.numberOfLines = 0;
            [re_wb setMinimumFontSize:14.0f];
            re_wb.frame = CGRectMake(30, size_body.height+100, 260, size_re_wb.height);
            [re_wb setFont:[UIFont systemFontOfSize:14.0f]];
            re_wb.text = re_wb_for_display;
            //NSURL *pic_URL = [NSURL URLWithString:[bsdata objectForKey:@"pic_url"]];
            //NSData* data = [[NSData alloc] initWithContentsOfURL:pic_URL];
            //UIImage *image = [[UIImage alloc] initWithData:data];
            NSLog(@"the clicked order is %i", _order);
            NSLog(@"the length of arrayImg is %i", [_arrayImg count]);
            UIImage *image = [_arrayImg objectAtIndex:_order];
            _pic.frame = CGRectMake(40, 100+size_body.height+size_re_wb.height, 240, 240*image.size.height/image.size.width);
            [_pic setImage:image];
            re_view.frame = CGRectZero;
            //re_view.frame = CGRectMake(20, size_body.height+100, 280, size_re_wb.height+_pic.frame.size.height);
            //re_view.backgroundColor = [UIColor colorWithRed:0.94 green:0.94 blue:0.94 alpha:1];
            
        }
        else{
            _pic.frame = CGRectZero;
            re_view.frame = CGRectZero;
            re_wb.frame = CGRectZero;
        }
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
    //self.view.frame= CGRectMake(0, 0, 300, 400);
}

- (void)viewDidUnload
{
//    [self setName:nil];
    [self setBodyField:nil];
//    [self setAvatar:nil];
    [self setPic:nil];
    [self setBsHeader:nil];
    [self setRe_wb:nil];
    [self setRe_view:nil];
    [self setArrayImg:nil];
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
//[self.delegate bsHeader:self clickedBS:_bs_id];
- (void)bsHeader:(BSHeader *)sender
       clickedBS:(int)BS_id{
    NSLog(@"mmmmm");
    //[self performSegueWithIdentifier:@"bsdetails" sender:self];
}

- (IBAction)click:(id)sender {
    [self dismissModalViewControllerAnimated:YES];
}

- (IBAction)go_bs:(id)sender {
    [self performSegueWithIdentifier:@"bsdetails" sender:self];
}

@end
