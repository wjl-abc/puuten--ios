//
//  MJDetailViewController.m
//  puuten
//
//  Created by wang jialei on 12-9-17.
//
//

#import "MJDetailViewController.h"

@interface MJDetailViewController ()

@end

@implementation MJDetailViewController
@synthesize wbBody=_wbBody;

-(void)setWbBody:(NSString *)wbBody{
    _wbBody =wbBody;
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
    CGRect body_frame = CGRectMake(30, 20, 230, 200);
    UILabel *body_label = [[UILabel alloc] initWithFrame:body_frame];
    body_label.backgroundColor = [UIColor clearColor];
    body_label.font = [UIFont fontWithName:@"CourierNewPSMT" size:14];
    body_label.numberOfLines = 10;
    body_label.text = _wbBody;
    
    [self.view addSubview:body_label];
    // Do any additional setup after loading the view from its nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    [self setWbBody:nil];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
